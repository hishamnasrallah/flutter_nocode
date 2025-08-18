# File: core/services/code_generation/services/api_service_generator.py
"""
Generates API service for Flutter applications.
"""

from ..base import BaseGenerator, GeneratorContext
from ..utils import StringUtils


class ApiServiceGenerator(BaseGenerator):
    """
    Generates API service layer for Flutter applications.
    """

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate API service file.

        Args:
            context: GeneratorContext containing data source information

        Returns:
            bool: True if successful
        """
        try:
            content = self._build_api_service_content(context)
            file_path = context.lib_path / 'services' / 'api_service.dart'
            return self.write_file(file_path, content, context)

        except Exception as e:
            self.add_error(f"Failed to generate API service: {str(e)}")
            return False

    def _build_api_service_content(self, context: GeneratorContext) -> str:
        """
        Build the API service content.

        Args:
            context: GeneratorContext containing data source information

        Returns:
            str: API service content
        """
        # Start with imports
        content = '''import 'dart:convert';
import 'package:http/http.dart' as http;'''

        # Add SharedPreferences import if using dynamic URLs
        if context.uses_dynamic_url:
            content += '''
import 'package:shared_preferences/shared_preferences.dart';'''

        # Add class definition
        content += '''

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();'''

        # Add URL management based on configuration
        if context.uses_dynamic_url:
            content += self._generate_dynamic_url_management()
        else:
            content += self._generate_static_url_management()

        # Generate methods for each data source
        content += self._generate_data_source_methods(context)

        # Add generic fetchData method
        content += self._generate_fetch_data_method(context)

        content += '\n}'

        return content

    def _generate_dynamic_url_management(self) -> str:
        """Generate dynamic URL management code."""
        return '''

  String? _cachedBaseUrl;

  // Get base URL - check saved configuration first, then use default
  Future<String> _getBaseUrl(String defaultUrl) async {
    // Return cached URL if available
    if (_cachedBaseUrl != null && _cachedBaseUrl!.isNotEmpty) {
      return _cachedBaseUrl!;
    }

    // Always check for saved URL first
    final prefs = await SharedPreferences.getInstance();
    final savedUrl = prefs.getString('base_url');

    // Check if base URL is special marker or if we should use saved URL
    if (defaultUrl == 'DYNAMIC' || defaultUrl.isEmpty) {
      if (savedUrl == null || savedUrl.isEmpty) {
        throw Exception('No server URL configured. Please configure the server URL first.');
      }
      _cachedBaseUrl = savedUrl;
      return _cachedBaseUrl!;
    }

    // Use saved URL if exists, otherwise use default from database
    _cachedBaseUrl = (savedUrl != null && savedUrl.isNotEmpty) ? savedUrl : defaultUrl;

    if (_cachedBaseUrl == null || _cachedBaseUrl!.isEmpty) {
      throw Exception('No server URL configured. Please configure the server URL first.');
    }

    return _cachedBaseUrl!;
  }

  // Clear cached URL when configuration changes
  void clearCache() {
    _cachedBaseUrl = null;
  }'''

    def _generate_static_url_management(self) -> str:
        """Generate static URL management code."""
        return '''

  // Simple static base URL
  Future<String> _getBaseUrl(String defaultUrl) async {
    return defaultUrl;
  }

  void clearCache() {
    // No-op for static configuration
  }'''

    def _generate_data_source_methods(self, context: GeneratorContext) -> str:
        """
        Generate methods for each data source.

        Args:
            context: GeneratorContext containing data sources

        Returns:
            str: Data source methods
        """
        content = ''

        for data_source in context.data_sources:
            method_name = 'fetch' + StringUtils.to_pascal_case(data_source.name)

            # Determine base URL parameter
            base_url_param = 'DYNAMIC' if data_source.use_dynamic_base_url else data_source.base_url

            content += f'''

    Future<dynamic> {method_name}() async {{
      try {{
        final baseUrl = await _getBaseUrl('{base_url_param}');
        final url = '${{baseUrl}}{data_source.endpoint}';
        final response = await http.{data_source.method.lower()}(
          Uri.parse(url),
          headers: {{
            'Content-Type': 'application/json','''

            # Add custom headers
            if data_source.headers:
                for line in data_source.headers.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        content += f"\n          '{key.strip()}': '{value.strip()}',"

            content += '''
          },
        );

        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          // Return data as-is, let the widgets handle the type
          return data;
        } else {
          throw Exception('Failed to load data: ${response.statusCode}');
        }
      } catch (e) {
        throw Exception('Network error: $e');
      }
    }'''

        return content

    def _generate_fetch_data_method(self, context: GeneratorContext) -> str:
        """
        Generate generic fetchData method.

        Args:
            context: GeneratorContext containing data sources

        Returns:
            str: fetchData method
        """
        content = '''

      Future<dynamic> fetchData(String dataSourceName) async {
        switch (dataSourceName) {'''

        for data_source in context.data_sources:
            method_name = 'fetch' + StringUtils.to_pascal_case(data_source.name)
            content += f"\n      case '{data_source.name}': return {method_name}();"

        content += '''
          default: throw Exception('Unknown data source: $dataSourceName');
        }
      }'''

        return content