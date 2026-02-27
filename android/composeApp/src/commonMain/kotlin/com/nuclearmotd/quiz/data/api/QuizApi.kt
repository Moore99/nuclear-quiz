package com.nuclearmotd.quiz.data.api

import com.nuclearmotd.quiz.data.api.debugBody
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.delete
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.client.statement.HttpResponse
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.http.isSuccess


class ApiException(val statusCode: Int, message: String) : Exception(message)

private const val BASE_URL = "https://quiz.nuclear-motd.com/api/"

class QuizApi(private val httpClient: HttpClient) {

    private suspend inline fun <reified T> HttpResponse.parse(): T {
        val raw = try {
            debugBody()
        } catch (_: Throwable) {
            "Could not read body"
        }

        if (!status.isSuccess()) {
            println("API ERROR ($status): $raw")
            throw ApiException(status.value, status.description)
        }

        return try {
            body<T>()
        } catch (e: Exception) {
            println("DESERIALIZATION ERROR for ${T::class.simpleName}: $e")
            println("RAW BODY: $raw")
            throw e
        }
    }

    suspend fun login(request: LoginRequest): AuthResponse =
        httpClient.post("${BASE_URL}auth/login") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.parse()

    suspend fun register(request: RegisterRequest): AuthResponse =
        httpClient.post("${BASE_URL}auth/register") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.parse()

    suspend fun resetPassword(request: ResetPasswordRequest): Unit =
        httpClient.post("${BASE_URL}auth/reset-password") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.parse()

    suspend fun changePassword(request: ChangePasswordRequest): Unit =
        httpClient.post("${BASE_URL}auth/change-password") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.parse()

    suspend fun deleteAccount(): Unit =
        httpClient.delete("${BASE_URL}auth/delete-account").parse()

    suspend fun getCategories(): List<Category> =
        httpClient.get("${BASE_URL}categories").parse()

    suspend fun startQuiz(request: StartQuizRequest): StartQuizResponse =
        httpClient.post("${BASE_URL}quiz/start") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.parse()

    suspend fun getQuestion(quizId: String): QuestionResponse =
        httpClient.get("${BASE_URL}quiz/$quizId").parse()

    suspend fun submitAnswer(quizId: String, request: AnswerRequest): AnswerResponse =
        httpClient.post("${BASE_URL}quiz/$quizId/answer") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.parse()

    suspend fun getResults(quizId: String): ResultsResponse =
        httpClient.get("${BASE_URL}quiz/$quizId/results").parse()

    suspend fun getProgress(): ProgressResponse =
        httpClient.get("${BASE_URL}progress").parse()
}
