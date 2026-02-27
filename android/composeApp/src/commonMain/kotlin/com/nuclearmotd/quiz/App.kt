package com.nuclearmotd.quiz

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.navigation.compose.rememberNavController
import com.nuclearmotd.quiz.data.prefs.TokenStore
import com.nuclearmotd.quiz.nav.NavGraph
import com.nuclearmotd.quiz.ui.theme.NuclearQuizTheme

@Composable
fun App(tokenStore: TokenStore) {
    remember { AppDependencies.init(tokenStore) }
    NuclearQuizTheme {
        NavGraph(rememberNavController())
    }
}
