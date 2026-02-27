package com.nuclearmotd.quiz.data.api

import io.ktor.client.statement.HttpResponse
import io.ktor.client.statement.bodyAsText

actual suspend fun HttpResponse.debugBody(): String = bodyAsText()