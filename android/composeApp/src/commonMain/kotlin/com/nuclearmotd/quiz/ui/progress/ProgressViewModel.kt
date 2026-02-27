package com.nuclearmotd.quiz.ui.progress

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ApiException
import com.nuclearmotd.quiz.data.api.ProgressResponse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ProgressViewModel : ViewModel() {

    private val api = AppDependencies.api

    private val _progressState = MutableStateFlow<UiState<ProgressResponse>>(UiState.Loading)
    val progressState: StateFlow<UiState<ProgressResponse>> = _progressState

    init {
        loadProgress()
    }

    fun loadProgress() {
        _progressState.value = UiState.Loading
        viewModelScope.launch {
            try {
                _progressState.value = UiState.Success(api.getProgress())
            } catch (e: ApiException) {
                _progressState.value = UiState.Error("Failed to load progress (${e.statusCode})")
            } catch (e: Exception) {
                _progressState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }
}
