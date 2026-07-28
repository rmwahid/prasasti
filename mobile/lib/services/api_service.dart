import 'package:dio/dio.dart';
import '../models/search_result.dart';

class ApiService {
  static const String baseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://localhost:8000',
  );

  final Dio _dio = Dio(BaseOptions(
    baseUrl: '$baseUrl/api/v1',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  Future<List<SearchMatch>> searchFace(String imagePath) async {
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(imagePath),
    });

    final response = await _dio.post('/search', data: formData);
    final matches = response.data['matches'] as List;
    return matches.map((m) => SearchMatch.fromJson(m)).toList();
  }
}
