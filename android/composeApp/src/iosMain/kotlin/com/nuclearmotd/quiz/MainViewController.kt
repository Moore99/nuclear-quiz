package com.nuclearmotd.quiz

import androidx.compose.ui.window.ComposeUIViewController
import com.nuclearmotd.quiz.data.prefs.IosTokenStore

fun MainViewController() = ComposeUIViewController {
    App(IosTokenStore())
}
