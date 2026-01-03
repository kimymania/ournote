import 'package:flutter/material.dart';
import 'package:ournote/views/login.dart';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPage();
}

class _SignupPage extends State<SignupPage> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _passwordCheckController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(30.0),
          child: Column(
            mainAxisAlignment: .center,
            crossAxisAlignment: .center,
            children: [
              Text(
                'Sign Up',
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontWeight: .bold,
                  fontSize: 26,
                  color: Color(0xFF1C1C1C),
                ),
              ),
              SizedBox(height: 6),
              Text(
                'Sign In to continue',
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontWeight: .normal,
                  fontSize: 18,
                  color: Color(0xFF1C1C1C),
                ),
              ),
              SizedBox(height: 26),
              TextField(
                controller: _usernameController,
                decoration: InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(),
                ),
              ),
              SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
              ),
              SizedBox(height: 16),
              TextField(
                controller: _passwordCheckController,
                decoration: InputDecoration(
                  labelText: 'Password Check',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
              ),
              SizedBox(height: 26),
              SizedBox(
                width: double.infinity,
                height: 49,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) {
                          return LoginPage();
                        },
                      ),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF3B62FF),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                  child: Text(
                    'Sign Up and Login',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: .bold,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
