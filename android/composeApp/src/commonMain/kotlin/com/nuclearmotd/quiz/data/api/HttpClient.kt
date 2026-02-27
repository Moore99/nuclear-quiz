package com.nuclearmotd.quiz.data.api

import com.nuclearmotd.quiz.data.prefs.TokenStore
import io.ktor.client.HttpClient
import io.ktor.client.HttpClientConfig
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.request.header
import io.ktor.http.HttpHeaders
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

expect fun createHttpClient(tokenStore: TokenStore): HttpClient

internal fun HttpClientConfig<*>.commonSetup(tokenStore: TokenStore) {
    install(ContentNegotiation) {
        json(Json { ignoreUnknownKeys = true })
    }
    
    defaultRequest {
        tokenStore.getToken()?.let {
            header(HttpHeaders.Authorization, "Bearer $it")
        }
    }
}
