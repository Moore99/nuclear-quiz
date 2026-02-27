package com.nuclearmotd.quiz.data.api

import io.ktor.client.statement.HttpResponse

expect suspend fun HttpResponse.debugBody(): String