import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'result_screen.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('PRASASTI'), centerTitle: true),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.face_retouching_natural, size: 80, color: Color(0xFF1a1a2e)),
            const SizedBox(height: 16),
            const Text('Photo Recognition Archive for\nSocial And Security Trace Intelligence',
                textAlign: TextAlign.center, style: TextStyle(fontSize: 14, color: Colors.grey)),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: () => _pickAndSearch(context, ImageSource.camera),
              icon: const Icon(Icons.camera_alt),
              label: const Text('Foto Wajah'),
              style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16)),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () => _pickAndSearch(context, ImageSource.gallery),
              icon: const Icon(Icons.photo_library),
              label: const Text('Upload dari Gallery'),
              style: OutlinedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16)),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _pickAndSearch(BuildContext context, ImageSource source) async {
    final picker = ImagePicker();
    final photo = await picker.pickImage(source: source);
    if (photo == null) return;
    if (context.mounted) {
      Navigator.push(context, MaterialPageRoute(builder: (_) => ResultScreen(imagePath: photo.path)));
    }
  }
}
