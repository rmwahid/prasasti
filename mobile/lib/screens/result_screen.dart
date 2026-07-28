import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';
import '../services/api_service.dart';
import '../models/search_result.dart';
import 'person_detail_screen.dart';

class ResultScreen extends StatefulWidget {
  final String imagePath;
  const ResultScreen({super.key, required this.imagePath});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  List<SearchMatch> _matches = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _search();
  }

  Future<void> _search() async {
    try {
      final results = await ApiService().searchFace(widget.imagePath);
      if (mounted) {
        setState(() {
          _matches = results;
          _loading = false;
        });
        _saveHistory();
      }
    } catch (e) {
      if (mounted) setState(() { _error = e.toString(); _loading = false; });
    }
  }

  Future<void> _saveHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final history = prefs.getStringList('search_history') ?? [];
    final entry = '${DateTime.now().toIso8601String()}|${widget.imagePath}';
    history.insert(0, entry);
    if (history.length > 50) history.removeRange(50, history.length);
    await prefs.setStringList('search_history', history);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Hasil Analisa')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Padding(padding: const EdgeInsets.all(24), child: Text(_error!, textAlign: TextAlign.center, style: const TextStyle(color: Colors.red))))
              : _matches.isEmpty
                  ? const Center(child: Text('Wajah tidak dikenali', style: TextStyle(fontSize: 16, color: Colors.grey)))
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: _matches.length,
                      itemBuilder: (context, index) {
                        final m = _matches[index];
                        final scoreColor = m.score >= 0.8 ? Colors.green : m.score >= 0.6 ? Colors.amber : Colors.red;
                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: InkWell(
                            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => PersonDetailScreen(match: m))),
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(children: [
                                    Expanded(child: Text(m.personName, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                      decoration: BoxDecoration(color: scoreColor.withValues(alpha: 0.15), borderRadius: BorderRadius.circular(12)),
                                      child: Text(m.confidencePercent, style: TextStyle(color: scoreColor, fontWeight: FontWeight.bold, fontSize: 14)),
                                    ),
                                  ]),
                                  if (m.personAlias != null)
                                    Padding(padding: const EdgeInsets.only(top: 4), child: Text('Alias: ${m.personAlias}', style: TextStyle(color: Colors.grey[600]))),
                                  if (m.score < 0.6)
                                    const Padding(
                                      padding: EdgeInsets.only(top: 8),
                                      child: Text('Kemungkinan salah orang', style: TextStyle(color: Colors.red, fontSize: 12, fontWeight: FontWeight.w500)),
                                    ),
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    ),
    );
  }
}
