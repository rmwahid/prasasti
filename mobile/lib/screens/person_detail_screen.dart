import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/search_result.dart';

class PersonDetailScreen extends StatelessWidget {
  final SearchMatch match;
  const PersonDetailScreen({super.key, required this.match});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(match.personName)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (match.personPhotoUrl != null)
              Center(child: ClipRRect(borderRadius: BorderRadius.circular(12), child: Image.network(match.personPhotoUrl!, height: 200, fit: BoxFit.cover))),
            const SizedBox(height: 16),
            if (match.personAlias != null)
              Text('Alias: ${match.personAlias}', style: TextStyle(color: Colors.grey[600], fontSize: 16)),
            const SizedBox(height: 24),
            const Text('Riwayat Kasus', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            if (match.cases.isEmpty)
              const Text('Belum ada data kasus.', style: TextStyle(color: Colors.grey)),
            ...match.cases.map((c) => Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (c.category != null)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        margin: const EdgeInsets.only(bottom: 6),
                        decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(8)),
                        child: Text(c.category!, style: const TextStyle(fontSize: 12)),
                      ),
                    Text(c.title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                    if (c.description != null) ...[
                      const SizedBox(height: 4),
                      Text(c.description!, style: TextStyle(color: Colors.grey[600], fontSize: 14)),
                    ],
                    if (c.caseDate != null)
                      Padding(padding: const EdgeInsets.only(top: 6), child: Text(c.caseDate!, style: const TextStyle(fontSize: 12, color: Colors.grey))),
                    if (c.sourceUrl != null)
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: InkWell(
                          onTap: () => launchUrl(Uri.parse(c.sourceUrl!)),
                          child: const Text('Lihat sumber', style: TextStyle(color: Colors.blue, fontSize: 13, decoration: TextDecoration.underline)),
                        ),
                      ),
                  ],
                ),
              ),
            )),
          ],
        ),
      ),
    );
  }
}
