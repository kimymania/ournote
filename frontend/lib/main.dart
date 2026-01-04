import 'package:flutter/material.dart';
import 'package:ournote/views/login.dart';
import 'package:ournote/globals.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login Page',
      theme: ThemeData(primarySwatch: Colors.lightGreen),
      home: const LoginPage(),
      navigatorKey: navigatorKey,
    );
  }
}
