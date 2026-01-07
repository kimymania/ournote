import 'package:flutter/material.dart';
import 'package:ournote/service.dart';
import 'package:ournote/models.dart';
import 'package:ournote/views/user.dart';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key, required this.apiService});
  final ApiService apiService;

  @override
  State<SignupPage> createState() => _SignupPage();
}

class _SignupPage extends State<SignupPage> {
  final _signupFormKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _passwordCheckController = TextEditingController();
  Token? token;
  bool _isLoading = false;

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    _passwordCheckController.dispose();
    super.dispose();
  }

  Future<void> _login(String username, String password) async {
    setState(() => _isLoading = true);

    try {
      token = await widget.apiService.getToken(username, password);
    } on Exception {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text("Failed to login")));
        return;
      }
    }

    setState(() => _isLoading = false);

    if (!mounted) return;
    if (token != null) {
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(
          builder: (context) => UserView(token: token!, username: username),
        ),
        (route) => false,
      );
    } else {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Invalid credentials!")));
    }
  }

  Future<void> _submit() async {
    final username = _usernameController.text;
    final password = _passwordCheckController.text;

    setState(() => _isLoading = true);

    if (!_signupFormKey.currentState!.validate()) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Error! Failed to validate input")));
    }

    try {
      await widget.apiService.createUser(username, password);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text("Error! Failed to create user")));
      }
    }

    _login(username, password);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(30.0),
          child: Form(
            key: _signupFormKey,
            child: Column(
              mainAxisAlignment: .center,
              crossAxisAlignment: .center,
              children: [
                const Text(
                  "Sign Up",
                  style: TextStyle(
                    fontFamily: "Poppins",
                    fontWeight: .bold,
                    fontSize: 26,
                    color: Color(0xFF1C1C1C),
                  ),
                ),
                const SizedBox(height: 6),
                const Text(
                  "Create new account",
                  style: TextStyle(
                    fontFamily: "Poppins",
                    fontWeight: .normal,
                    fontSize: 18,
                    color: Color(0xFF1C1C1C),
                  ),
                ),
                const SizedBox(height: 26),
                TextFormField(
                  validator: (value) {
                    return value!.isEmpty ? "Enter a username" : null;
                  },
                  controller: _usernameController,
                  decoration: const InputDecoration(
                    labelText: "Username",
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                TextFormField(
                  validator: (value) {
                    return value!.isEmpty ? "Enter a password" : null;
                  },
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: "Password",
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  validator: (value) {
                    if (value!.isEmpty) {
                      return "Re-enter the password";
                    } else if (value != _passwordController.text) {
                      return "Password doesn't match";
                    } else {
                      return null;
                    }
                  },
                  controller: _passwordCheckController,
                  decoration: const InputDecoration(
                    labelText: "Password Check",
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 26),
                SizedBox(
                  width: double.infinity,
                  height: 49,
                  child: ElevatedButton(
                    onPressed: () => _submit(),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFF3B62FF),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    child: const Text(
                      "Sign Up and Login",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: .bold,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Center(
                  child: TextButton(
                    child: Text(
                      "I already have an account",
                      textAlign: .center,
                      style: TextStyle(fontSize: 14, color: Color(0xFF87879D)),
                    ),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
