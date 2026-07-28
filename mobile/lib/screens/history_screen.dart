import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<Map<String, String>> _history = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList('search_history') ?? [];
    setState(() {
      _history = raw.map((e) {
        final parts = e.split('|');
        return {'date': parts[0], 'path': parts[1]};
      }).toList();
    });
  }

  Future<void> _clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('search_history');
    _loadHistory();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Riwayat'), actions: [
        if (_history.isNotEmpty)
          IconButton(onPressed: _clearHistory, icon: const Icon(Icons.delete_outline)),
      ]),
      body: _history.isEmpty
          ? const Center(child: Text('Belum ada riwayat.', style: TextStyle(color: Colors.grey)))
          : ListView.builder(
              itemCount: _history.length,
              itemBuilder: (context, index) {
                final item = _history[index];
                final dt = DateTime.tryParse(item['date'] ?? '');
                return ListTile(
                  leading: const Icon(Icons.history, color: Colors.grey),
                  title: Text(dt != null ? dt.toString().substring(0, 19) : item['date']!),
                  subtitle: Text(item['path']!, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12)),
                );
              },
            ),
    );
  }
}
