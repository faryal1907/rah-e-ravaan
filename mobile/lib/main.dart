import 'package:flutter/material.dart';

void main() {
  runApp(const RahERavaanApp());
}

class RahERavaanApp extends StatelessWidget {
  const RahERavaanApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rah-e-Ravaan',
      home: Scaffold(
        body: Center(
          child: Text(
            'Rah-e-Ravaan',
            style: TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}