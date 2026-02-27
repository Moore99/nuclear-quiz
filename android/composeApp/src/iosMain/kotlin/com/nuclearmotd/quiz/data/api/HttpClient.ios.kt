package com.nuclearmotd.quiz.data.api

import com.nuclearmotd.quiz.data.prefs.TokenStore
import io.ktor.client.HttpClient
import io.ktor.client.engine.darwin.Darwin

actual fun createHttpClient(tokenStore: TokenStore): HttpClient = HttpClient(Darwin) {
    commonSetup(tokenStore)
}
