import requests
import json
import os
from pathlib import Path
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from ..models import Application, BuildHistory
from .code_generator import FlutterCodeGenerator


class BuildService:
    """Handles building Flutter applications into APK files"""
    
    def __init__(self):
        self.build_server_url = settings.BUILD_SERVER_URL
        self.api_key = settings.BUILD_SERVER_API_KEY
    
    def start_build(self, application):
        """Start the build process for an application"""
        try:
            # Create build history record
            build_history = BuildHistory.objects.create(
                application=application,
                status='started'
            )
            
            # Update application status
            application.build_status = 'building'
            application.save()
            
            # Generate Flutter code first
            build_history.status = 'generating_code'
            build_history.save()
            
            generator = FlutterCodeGenerator(application)
            success, message = generator.generate_project()
            
            if not success:
                build_history.status = 'code_generation_failed'
                build_history.error_message = message
                build_history.build_end_time = timezone.now()
                build_history.save()
                
                application.build_status = 'failed'
                application.save()
                
                return False, f"Code generation failed: {message}"
            
            build_history.status = 'code_generated'
            build_history.log_output = f"Code generation successful: {message}\n"
            build_history.save()
            
            # For now, simulate APK build since we don't have a real build server
            # In production, this would send the project to a Flutter build server
            success, apk_path = self._simulate_apk_build(application, build_history)
            
            if success:
                build_history.status = 'success'
                build_history.build_end_time = timezone.now()
                build_history.log_output += "APK build completed successfully\n"
                
                # Save APK file to build history and application
                with open(apk_path, 'rb') as apk_file:
                    apk_content = ContentFile(apk_file.read())
                    apk_filename = f"{application.package_name}.apk"
                    
                    build_history.apk_file.save(apk_filename, apk_content)
                    application.apk_file.save(apk_filename, apk_content)
                
                # Calculate APK size
                build_history.apk_size_mb = round(os.path.getsize(apk_path) / (1024 * 1024), 2)
                build_history.save()
                
                application.build_status = 'success'
                application.save()
                
                return True, "APK build completed successfully"
            else:
                build_history.status = 'failed'
                build_history.error_message = apk_path  # Error message in this case
                build_history.build_end_time = timezone.now()
                build_history.save()
                
                application.build_status = 'failed'
                application.save()
                
                return False, f"APK build failed: {apk_path}"
                
        except Exception as e:
            # Update build history with error
            if 'build_history' in locals():
                build_history.status = 'failed'
                build_history.error_message = str(e)
                build_history.build_end_time = timezone.now()
                build_history.save()
            
            application.build_status = 'failed'
            application.save()
            
            return False, f"Build process failed: {str(e)}"
    
    def _simulate_apk_build(self, application, build_history):
        """Build APK using configured Flutter SDK"""
        import subprocess
        import shutil

        try:
            # Check if we should use mock build (for testing)
            if settings.USE_MOCK_BUILD:
                apk_path = settings.APK_STORAGE_PATH / f"{application.package_name}.apk"
                with open(apk_path, 'w') as f:
                    f.write("Mock APK for testing")
                return True, apk_path

            # Check if Flutter is available using settings
            if not hasattr(settings, 'FLUTTER_AVAILABLE') or not settings.FLUTTER_AVAILABLE:
                return False, f"Flutter SDK not found. Please check your FLUTTER_SDK_PATH setting."

            # Use Flutter SDK from settings
            project_path = settings.GENERATED_CODE_PATH / f"{application.package_name.replace('.', '_')}"
            flutter_exe = os.path.join(settings.FLUTTER_SDK_PATH, 'bin', 'flutter.bat' if os.name == 'nt' else 'flutter')

            if not project_path.exists():
                return False, f"Project path not found: {project_path}"

            build_history.log_output += f"Using Flutter SDK: {settings.FLUTTER_SDK_PATH}\n"
            build_history.log_output += f"Building project at: {project_path}\n"
            build_history.save()

            # Step 1: Clean previous builds and kill any lingering processes
            build_history.status = 'building_apk'
            build_history.log_output += "Cleaning previous builds...\n"
            build_history.save()

            # On Windows, kill any lingering Java/Gradle processes
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/IM', 'java.exe'],
                             capture_output=True, shell=True)
                subprocess.run(['taskkill', '/F', '/IM', 'gradle.exe'],
                             capture_output=True, shell=True)
                import time
                time.sleep(1)  # Give time for processes to terminate

            # Clean the build directory manually first
            build_dir = project_path / 'build'
            if build_dir.exists():
                try:
                    shutil.rmtree(build_dir, ignore_errors=True)
                    build_history.log_output += "Removed old build directory\n"
                except Exception as e:
                    build_history.log_output += f"Warning: Could not fully clean build dir: {e}\n"

            # Now run Flutter clean
            result = subprocess.run(
                [flutter_exe, 'clean'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120,
                env=os.environ.copy()
            )

            if result.returncode != 0:
                build_history.log_output += f"Warning: Flutter clean failed: {result.stderr}\n"
                # Continue anyway as we already cleaned manually

            # Step 2: Get dependencies
            build_history.log_output += "Installing dependencies (flutter pub get)...\n"
            build_history.save()

            result = subprocess.run(
                [flutter_exe, 'pub', 'get'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300,
                env=os.environ.copy()
            )

            if result.returncode != 0:
                error_msg = f"Flutter pub get failed:\n{result.stderr}"
                build_history.log_output += error_msg + "\n"
                build_history.save()
                return False, error_msg

            build_history.log_output += "Dependencies installed successfully\n"
            build_history.save()

            # Step 3: Run flutter doctor first to check environment
            build_history.log_output += "\n=== Running Flutter Doctor ===\n"
            build_history.save()

            doctor_result = subprocess.run(
                [flutter_exe, 'doctor', '-v'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=60,
                env=os.environ.copy()
            )

            build_history.log_output += doctor_result.stdout[:2000] + "\n"
            build_history.save()

            # Step 4: Create Android project files if missing
            build_history.log_output += "\n=== Creating Android project files ===\n"
            build_history.save()

            create_result = subprocess.run(
                [flutter_exe, 'create', '.', '--platforms=android'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120,
                env=os.environ.copy()
            )

            if create_result.stdout:
                build_history.log_output += create_result.stdout[:1000] + "\n"
            build_history.save()

            # Step 5: Build APK
            build_history.log_output += "\n=== Building APK (this may take 3-5 minutes) ===\n"
            build_history.save()

            # Use BUILD_TIMEOUT from settings
            timeout = getattr(settings, 'BUILD_TIMEOUT', 600)

            # First try to analyze the code for errors
            analyze_result = subprocess.run(
                [flutter_exe, 'analyze', '--no-fatal-warnings'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=60,
                env=os.environ.copy()
            )

            if analyze_result.returncode != 0:
                build_history.log_output += f"\n=== Code Analysis Errors ===\n{analyze_result.stdout}\n"
                build_history.save()

            # Build APK without verbose flag first to get cleaner error messages
            result = subprocess.run(
                [flutter_exe, 'build', 'apk', '--release'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=os.environ.copy()
            )

            # Log output - look for actual Dart errors
            if result.returncode != 0:
                # Extract the actual error from stdout
                output_lines = result.stdout.split('\n') if result.stdout else []
                error_lines = []
                capture_error = False

                for line in output_lines:
                    if 'Error:' in line or 'error:' in line:
                        capture_error = True
                    if capture_error:
                        error_lines.append(line)
                        if line.strip() == '' and len(error_lines) > 5:
                            break  # Stop after getting the main error

                if error_lines:
                    build_history.log_output += f"\n=== Dart Compilation Error ===\n"
                    build_history.log_output += '\n'.join(error_lines) + "\n"
                else:
                    # Fall back to full output if no specific error found
                    build_history.log_output += f"\n=== Build Output (Last 10000 chars) ===\n"
                    build_history.log_output += result.stdout[-10000:] if result.stdout else "No stdout"
                    build_history.log_output += f"\n=== Build Errors ===\n"
                    build_history.log_output += result.stderr[-5000:] if result.stderr else "No stderr"
            else:
                # Success - just log summary
                build_history.log_output += "\n✅ Build completed successfully\n"

            # Save the log so we can see it in admin
            build_history.save()

            if result.returncode == 0:
                # Find the built APK - check multiple possible locations
                apk_locations = [
                    project_path / 'build' / 'app' / 'outputs' / 'flutter-apk' / 'app-release.apk',
                    project_path / 'build' / 'app' / 'outputs' / 'apk' / 'release' / 'app-release.apk',
                ]

                apk_source = None
                for location in apk_locations:
                    if location.exists():
                        apk_source = location
                        build_history.log_output += f"Found APK at: {location}\n"
                        break

                if apk_source:
                    apk_dest = settings.APK_STORAGE_PATH / f"{application.package_name}.apk"
                    shutil.copy2(apk_source, apk_dest)

                    # Calculate APK size
                    apk_size = os.path.getsize(apk_source)
                    apk_size_mb = round(apk_size / (1024 * 1024), 2)

                    build_history.log_output += f"\n✅ APK built successfully!\n"
                    build_history.log_output += f"Size: {apk_size_mb} MB\n"
                    build_history.log_output += f"Saved to: {apk_dest}\n"
                    build_history.apk_size_mb = apk_size_mb
                    build_history.save()

                    return True, apk_dest
                else:
                    error_msg = "APK file not found after build. Check paths:\n"
                    for location in apk_locations:
                        error_msg += f"  - {location} (exists: {location.exists()})\n"
                    build_history.log_output += error_msg
                    build_history.save()
                    return False, error_msg
            else:
                error_msg = f"Flutter build failed with exit code {result.returncode}"
                build_history.log_output += f"\n❌ {error_msg}\n"
                build_history.save()
                return False, error_msg

        except subprocess.TimeoutExpired:
            timeout = getattr(settings, 'BUILD_TIMEOUT', 600)
            error_msg = f"Build process timed out after {timeout} seconds"
            build_history.log_output += f"\n❌ {error_msg}\n"
            build_history.save()
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            build_history.log_output += f"\n❌ {error_msg}\n"
            import traceback
            build_history.log_output += f"Traceback:\n{traceback.format_exc()}\n"
            build_history.save()
            return False, error_msg
    
    def _send_to_build_server(self, project_zip_path, application, build_history):
        """Send project to build server (for real implementation)"""
        try:
            # This would be implemented when you have a real build server
            build_endpoint = f"{self.build_server_url}/api/build"
            
            with open(project_zip_path, 'rb') as zip_file:
                files = {'project': zip_file}
                data = {
                    'package_name': application.package_name,
                    'app_name': application.name,
                    'version': application.version,
                    'build_id': str(build_history.build_id),
                }
                headers = {
                    'Authorization': f'Bearer {self.api_key}'
                }
                
                response = requests.post(
                    build_endpoint,
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=300  # 5 minutes timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return True, result.get('apk_url'), result.get('logs', '')
                else:
                    return False, f"Build server error: {response.status_code}", response.text
                    
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}", ""
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", ""
    
    def get_build_status(self, application):
        """Get current build status"""
        latest_build = application.build_history.first()
        
        return {
            'application_status': application.build_status,
            'latest_build': {
                'id': str(latest_build.build_id) if latest_build else None,
                'status': latest_build.status if latest_build else None,
                'start_time': latest_build.build_start_time if latest_build else None,
                'end_time': latest_build.build_end_time if latest_build else None,
                'duration': latest_build.duration_seconds if latest_build else None,
                'error_message': latest_build.error_message if latest_build else None,
                'apk_available': bool(latest_build.apk_file) if latest_build else False,
                'source_available': bool(latest_build.source_code_zip) if latest_build else False,
            } if latest_build else None
        }