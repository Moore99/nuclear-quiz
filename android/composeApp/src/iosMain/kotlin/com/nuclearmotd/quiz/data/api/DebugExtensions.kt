package com.nuclearmotd.quiz.data.api

import io.ktor.client.statement.HttpResponse

actual suspend fun HttpResponse.debugBody(): String = ""