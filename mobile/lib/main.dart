import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const ProviderScope(child: PrasastiApp()));
}

class PrasastiApp extends StatelessWidget {
  const PrasastiApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Prasasti',
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFF1a1a2e),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
