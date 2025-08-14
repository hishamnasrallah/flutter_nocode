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
        """Simulate APK build process (for demonstration)"""
        try:
            # In a real implementation, this would:
            # 1. ZIP the generated Flutter project
            # 2. Send it to a build server with Flutter SDK
            # 3. Run 'flutter build apk --release'
            # 4. Return the built APK file
            
            # For now, create a dummy APK file
            apk_path = settings.APK_STORAGE_PATH / f"{application.package_name}.apk"
            
            # Create a simple dummy APK (just a text file for demonstration)
            dummy_apk_content = f"""
This is a simulated APK file for {application.name}
Package: {application.package_name}
Version: {application.version}
Build ID: {build_history.build_id}
Generated at: {timezone.now()}

In a real implementation, this would be a proper Android APK file
built from the generated Flutter source code.

To implement real APK building:
1. Set up a build server with Flutter SDK
2. Implement API endpoints to receive Flutter projects
3. Run 'flutter build apk --release' on the server
4. Return the built APK file

The generated Flutter source code is available in the source ZIP file.
"""
            
            with open(apk_path, 'w') as f:
                f.write(dummy_apk_content)
            
            return True, apk_path
            
        except Exception as e:
            return False, str(e)
    
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