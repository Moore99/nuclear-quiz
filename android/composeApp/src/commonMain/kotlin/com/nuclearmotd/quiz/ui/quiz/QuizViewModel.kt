package com.nuclearmotd.quiz.ui.quiz

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ApiException
import com.nuclearmotd.quiz.data.api.AnswerRequest
import com.nuclearmotd.quiz.data.api.AnswerResponse
import com.nuclearmotd.quiz.data.api.QuestionResponse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class QuizViewModel : ViewModel() {

    private val api = AppDependencies.api

    private val _questionState = MutableStateFlow<UiState<QuestionResponse>>(UiState.Loading)
    val questionState: StateFlow<UiState<QuestionResponse>> = _questionState

    private val _answerState = MutableStateFlow<AnswerResponse?>(null)
    val answerState: StateFlow<AnswerResponse?> = _answerState

    private val _isSubmitting = MutableStateFlow(false)
    val isSubmitting: StateFlow<Boolean> = _isSubmitting

    private var quizId: String = ""

    fun init(quizId: String) {
        this.quizId = quizId
        loadQuestion()
    }

    fun loadQuestion() {
        _questionState.value = UiState.Loading
        _answerState.value = null
        viewModelScope.launch {
            try {
                _questionState.value = UiState.Success(api.getQuestion(quizId))
            } catch (e: ApiException) {
                _questionState.value = UiState.Error("Failed to load question (${e.statusCode})")
            } catch (e: Exception) {
                _questionState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun submitAnswer(answerId: Int) {
        val currentQuestion = (questionState.value as? UiState.Success)?.data ?: return
        
        if (_isSubmitting.value) return
        _isSubmitting.value = true
        viewModelScope.launch {
            try {
                _answerState.value = api.submitAnswer(
                    quizId, 
                    AnswerRequest(answerId = answerId, questionId = currentQuestion.questionId)
                )
            } catch (e: ApiException) {
                _questionState.value = UiState.Error("Failed to submit answer (${e.statusCode})")
            } catch (e: Exception) {
                _questionState.value = UiState.Error("Network error: ${e.message}")
            } finally {
                _isSubmitting.value = false
            }
        }
    }

    fun dismissAnswer() {
        _answerState.value = null
    }
}
