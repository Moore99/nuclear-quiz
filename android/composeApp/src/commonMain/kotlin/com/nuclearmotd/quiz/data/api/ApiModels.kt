package com.nuclearmotd.quiz.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

// ── Auth & Account ───────────────────────────────────────────────────────────

@Serializable
data class LoginRequest(
    val username: String,
    val password: String
)

@Serializable
data class RegisterRequest(
    val username: String,
    val password: String
)

@Serializable
data class ForgotPasswordRequest(
    val username: String
)

@Serializable
data class ChangePasswordRequest(
    @SerialName("current_password") val currentPassword: String,
    @SerialName("new_password") val newPassword: String
)

@Serializable
data class AuthResponse(
    val token: String,
    val username: String? = null,
    @SerialName("user_id") val userId: Int
)

// ── Categories ────────────────────────────────────────────────────────────────

@Serializable
data class Category(
    val id: Int,
    val name: String,
    val description: String? = null,
    val icon: String? = null,
    @SerialName("question_count") val questionCount: Int
)

// ── Quiz session ──────────────────────────────────────────────────────────────

@Serializable
data class StartQuizRequest(
    @SerialName("category_id") val categoryId: Int?,
    @SerialName("question_count") val questionCount: Int = 10
)

@Serializable
data class StartQuizResponse(
    @SerialName("quiz_id") val quizId: String,
    @SerialName("total_questions") val questionCount: Int,
    @SerialName("category_name") val categoryName: String? = null
)

// ── Question ──────────────────────────────────────────────────────────────────

@Serializable
data class AnswerOption(
    @SerialName("answer_text") val text: String,
    val id: Int
)

@Serializable
data class QuestionResponse(
    @SerialName("question_id") val questionId: Int,
    @SerialName("question_number") val questionNumber: Int,
    @SerialName("total_questions") val totalQuestions: Int,
    @SerialName("question_text") val question: String,
    val answers: List<AnswerOption>,
    @SerialName("is_complete") val isComplete: Boolean = false
)

// ── Answer ────────────────────────────────────────────────────────────────────

@Serializable
data class AnswerRequest(
    @SerialName("answer_id") val answerId: Int,
    @SerialName("question_id") val questionId: Int
)

@Serializable
data class AnswerResponse(
    @SerialName("is_correct") val correct: Boolean,
    @SerialName("correct_answer_text") val correctAnswer: String,
    val explanation: String?,
    @SerialName("is_complete") val isComplete: Boolean = false,
    val score: Int = 0,
    @SerialName("questions_answered") val questionsAnswered: Int = 0,
    @SerialName("total_questions") val totalQuestions: Int = 0
)

// ── Results ───────────────────────────────────────────────────────────────────

@Serializable
data class ReviewItem(
    @SerialName("question_text") val questionText: String,
    @SerialName("user_answer") val userAnswer: String,
    @SerialName("correct_answer") val correctAnswer: String,
    @SerialName("is_correct") val isCorrect: Boolean,
    val explanation: String? = null,
    val source: String? = null
)

@Serializable
data class QuizResult(
    @SerialName("quiz_id") val quizId: String,
    @SerialName("score") val score: Int = 0,
    @SerialName("total_questions") val totalQuestions: Int = 0,
    val percentage: Double = 0.0,
    @SerialName("category_name") val category: String? = null,
    @SerialName("completed_at") val completedAt: String? = null
)

@Serializable
data class ResultsResponse(
    @SerialName("quiz_id") val quizId: String,
    @SerialName("score") private val _score: Int? = null,
    @SerialName("total_questions") private val _totalQuestions: Int? = null,
    val percentage: Double = 0.0,
    @SerialName("category_name") val category: String? = null,
    @SerialName("completed_at") val completedAt: String? = null,
    val review: List<ReviewItem>? = null
) {
    val totalQuestions: Int get() = _totalQuestions ?: review?.size ?: 10
    val score: Int get() = _score ?: review?.count { it.isCorrect } ?: 0
}

// ── Progress ──────────────────────────────────────────────────────────────────

@Serializable
data class CategoryProgress(
    @SerialName("category_id") val categoryId: Int,
    @SerialName("category_name") val categoryName: String,
    @SerialName("total_answered") val totalAnswered: Int,
    @SerialName("total_correct") val totalCorrect: Int,
    val accuracy: Double
)

@Serializable
data class OverallProgress(
    @SerialName("total_answered") val totalAnswered: Int,
    @SerialName("total_correct") val totalCorrect: Int,
    val accuracy: Double
)

@Serializable
data class ProgressResponse(
    @SerialName("by_category") val byCategory: List<CategoryProgress>,
    val overall: OverallProgress
)
