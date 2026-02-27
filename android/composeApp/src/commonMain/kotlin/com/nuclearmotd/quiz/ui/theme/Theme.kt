package com.nuclearmotd.quiz.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val NuclearGreen = Color(0xFF00C853)
private val NuclearGreenDark = Color(0xFF009624)
private val NuclearYellow = Color(0xFFFFD600)

private val LightColors = lightColorScheme(
    primary = NuclearGreenDark,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFB9F6CA),
    onPrimaryContainer = Color(0xFF00210C),
    secondary = NuclearYellow,
    onSecondary = Color.Black,
    background = Color(0xFFF5F5F5),
    surface = Color.White,
    onBackground = Color(0xFF1A1A1A),
    onSurface = Color(0xFF1A1A1A),
)

private val DarkColors = darkColorScheme(
    primary = NuclearGreen,
    onPrimary = Color.Black,
    primaryContainer = NuclearGreenDark,
    onPrimaryContainer = Color(0xFFB9F6CA),
    secondary = NuclearYellow,
    onSecondary = Color.Black,
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    onBackground = Color(0xFFE0E0E0),
    onSurface = Color(0xFFE0E0E0),
)

@Composable
fun NuclearQuizTheme(
    darkTheme: Boolean = false,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content
    )
}
