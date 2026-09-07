import 'package:flutter/material.dart';

enum MascotState { idle, waving, celebrating, aiThinking, error404, thumbsUp, sleeping }

class ByteBotMascot extends StatelessWidget {
  final MascotState state;
  final double size;
  final bool animated;
  final VoidCallback? onTap;

  const ByteBotMascot({
    super.key,
    this.state = MascotState.idle,
    this.size = 180.0,
    this.animated = true,
    this.onTap,
  });

  String get _assetPath {
    final suffix = animated ? '_animated.webp' : '_transparent.png';
    switch (state) {
      case MascotState.idle:
      case MascotState.waving:
        return 'assets/processed/waving$suffix';
      case MascotState.celebrating:
        return 'assets/processed/celebrating$suffix';
      case MascotState.aiThinking:
        return 'assets/processed/ai_thinking$suffix';
      case MascotState.error404:
        return 'assets/processed/error_404$suffix';
      case MascotState.thumbsUp:
        return 'assets/processed/thumbs_up$suffix';
      case MascotState.sleeping:
        return 'assets/processed/sleeping$suffix';
    }
  }

  Color get _glowColor {
    switch (state) {
      case MascotState.idle:
      case MascotState.waving:
        return const Color(0xFF06B6D4);
      case MascotState.celebrating:
        return const Color(0xFFF59E0B);
      case MascotState.aiThinking:
        return const Color(0xFF3B82F6);
      case MascotState.error404:
        return const Color(0xFFEF4444);
      case MascotState.thumbsUp:
        return const Color(0xFF10B981);
      case MascotState.sleeping:
        return const Color(0xFF8B5CF6);
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(
              color: _glowColor.withOpacity(0.35),
              blurRadius: 30,
              spreadRadius: 5,
            )
          ],
        ),
        child: Image.asset(
          _assetPath,
          fit: BoxFit.contain,
        ),
      ),
    );
  }
}
