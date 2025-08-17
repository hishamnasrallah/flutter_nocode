# File: core/services/code_generation/services/model_generator.py
"""
Generates data models for Flutter applications.
"""

from ..base import BaseGenerator, GeneratorContext


class ModelGenerator(BaseGenerator):
    """
    Generates data model classes for Flutter applications.
    """

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate data models file.

        Args:
            context: GeneratorContext containing application information

        Returns:
            bool: True if successful
        """
        try:
            content = self._build_models_content(context)
            file_path = context.lib_path / 'models' / 'app_models.dart'
            return self.write_file(file_path, content, context)

        except Exception as e:
            self.add_error(f"Failed to generate models: {str(e)}")
            return False

    def _build_models_content(self, context: GeneratorContext) -> str:
        """
        Build the data models content.

        Args:
            context: GeneratorContext containing application information

        Returns:
            str: Models file content
        """
        content = '''// Data models for the application

class AppData {
  final Map<String, dynamic> data;

  AppData(this.data);

  factory AppData.fromJson(Map<String, dynamic> json) {
    return AppData(json);
  }

  Map<String, dynamic> toJson() {
    return data;
  }

  dynamic operator [](String key) => data[key];
  void operator []=(String key, dynamic value) => data[key] = value;
}

class ApiResponse<T> {
  final bool success;
  final T? data;
  final String? error;
  final int? statusCode;

  ApiResponse({
    required this.success,
    this.data,
    this.error,
    this.statusCode,
  });

  factory ApiResponse.success(T data, [int statusCode = 200]) {
    return ApiResponse(
      success: true,
      data: data,
      statusCode: statusCode,
    );
  }

  factory ApiResponse.error(String error, [int statusCode = 500]) {
    return ApiResponse(
      success: false,
      error: error,
      statusCode: statusCode,
    );
  }
}

class ListItem {
  final String? id;
  final String? title;
  final String? description;
  final String? imageUrl;
  final Map<String, dynamic> extras;

  ListItem({
    this.id,
    this.title,
    this.description,
    this.imageUrl,
    Map<String, dynamic>? extras,
  }) : extras = extras ?? {};

  factory ListItem.fromJson(Map<String, dynamic> json) {
    return ListItem(
      id: json['id']?.toString(),
      title: json['title']?.toString() ?? json['name']?.toString(),
      description: json['description']?.toString(),
      imageUrl: json['imageUrl']?.toString() ?? json['image']?.toString(),
      extras: json,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      if (title != null) 'title': title,
      if (description != null) 'description': description,
      if (imageUrl != null) 'imageUrl': imageUrl,
      ...extras,
    };
  }
}

class Category {
  final String? id;
  final String? name;
  final String? icon;
  final String? image;
  final String? description;
  final int? itemCount;

  Category({
    this.id,
    this.name,
    this.icon,
    this.image,
    this.description,
    this.itemCount,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id']?.toString(),
      name: json['name']?.toString(),
      icon: json['icon']?.toString(),
      image: json['image']?.toString(),
      description: json['description']?.toString(),
      itemCount: json['itemCount'] != null ? int.tryParse(json['itemCount'].toString()) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      if (name != null) 'name': name,
      if (icon != null) 'icon': icon,
      if (image != null) 'image': image,
      if (description != null) 'description': description,
      if (itemCount != null) 'itemCount': itemCount,
    };
  }
}

class User {
  final String? id;
  final String? name;
  final String? email;
  final String? avatarUrl;
  final Map<String, dynamic> metadata;

  User({
    this.id,
    this.name,
    this.email,
    this.avatarUrl,
    Map<String, dynamic>? metadata,
  }) : metadata = metadata ?? {};

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id']?.toString(),
      name: json['name']?.toString(),
      email: json['email']?.toString(),
      avatarUrl: json['avatarUrl']?.toString() ?? json['avatar']?.toString(),
      metadata: json,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      if (name != null) 'name': name,
      if (email != null) 'email': email,
      if (avatarUrl != null) 'avatarUrl': avatarUrl,
      ...metadata,
    };
  }
}

// Generic model for handling any data structure
class DynamicModel {
  final Map<String, dynamic> _data;

  DynamicModel(this._data);

  factory DynamicModel.fromJson(Map<String, dynamic> json) {
    return DynamicModel(json);
  }

  Map<String, dynamic> toJson() => _data;

  // Dynamic property access
  dynamic get(String key) => _data[key];
  void set(String key, dynamic value) => _data[key] = value;
  bool has(String key) => _data.containsKey(key);

  // Typed getters with null safety
  String? getString(String key) => _data[key]?.toString();
  int? getInt(String key) {
    final value = _data[key];
    if (value == null) return null;
    if (value is int) return value;
    return int.tryParse(value.toString());
  }

  double? getDouble(String key) {
    final value = _data[key];
    if (value == null) return null;
    if (value is double) return value;
    if (value is int) return value.toDouble();
    return double.tryParse(value.toString());
  }

  bool? getBool(String key) {
    final value = _data[key];
    if (value == null) return null;
    if (value is bool) return value;
    final strValue = value.toString().toLowerCase();
    return strValue == 'true' || strValue == '1';
  }

  List<dynamic>? getList(String key) {
    final value = _data[key];
    if (value == null) return null;
    if (value is List) return value;
    return null;
  }

  Map<String, dynamic>? getMap(String key) {
    final value = _data[key];
    if (value == null) return null;
    if (value is Map<String, dynamic>) return value;
    return null;
  }
}
'''

        return content