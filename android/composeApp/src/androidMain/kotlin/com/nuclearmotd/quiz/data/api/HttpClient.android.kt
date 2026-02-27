package com.nuclearmotd.quiz.data.api

import com.nuclearmotd.quiz.data.prefs.TokenStore
import io.ktor.client.HttpClient
import io.ktor.client.engine.okhttp.OkHttp

actual fun createHttpClient(tokenStore: TokenStore): HttpClient = HttpClient(OkHttp) {
    commonSetup(tokenStore)
}
