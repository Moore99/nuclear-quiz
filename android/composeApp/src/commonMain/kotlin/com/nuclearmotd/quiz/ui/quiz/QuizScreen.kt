package com.nuclearmotd.quiz.ui.quiz

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.AnswerResponse
import com.nuclearmotd.quiz.data.api.QuestionResponse

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuizScreen(
    quizId: String,
    onComplete: (String) -> Unit,
    onBack: () -> Unit,
    vm: QuizViewModel = viewModel()
) {
    val questionState by vm.questionState.collectAsState()
    val answerState by vm.answerState.collectAsState()
    val isSubmitting by vm.isSubmitting.collectAsState()

    LaunchedEffect(quizId) {
        vm.init(quizId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Quiz") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when (val state = questionState) {
                is UiState.Loading -> {
                    CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                }
                is UiState.Error -> {
                    Column(
                        modifier = Modifier.align(Alignment.Center).padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(state.message, color = MaterialTheme.colorScheme.error, textAlign = TextAlign.Center)
                        Spacer(Modifier.height(16.dp))
                        Button(onClick = { vm.loadQuestion() }) { Text("Retry") }
                    }
                }
                is UiState.Success -> {
                    QuestionContent(
                        question = state.data,
                        isSubmitting = isSubmitting,
                        onAnswer = { vm.submitAnswer(it) }
                    )
                }
            }

            answerState?.let { result ->
                AnswerOverlay(
                    result = result,
                    onDismiss = {
                        if (result.isComplete) {
                            onComplete(quizId)
                        } else {
                            vm.dismissAnswer()
                            vm.loadQuestion()
                        }
                    }
                )
            }
        }
    }
}

@Composable
private fun QuestionContent(
    question: QuestionResponse,
    isSubmitting: Boolean,
    onAnswer: (Int) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState())
    ) {
        LinearProgressIndicator(
            progress = { question.questionNumber.toFloat() / question.totalQuestions },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(4.dp))
        Text(
            text = "Question ${question.questionNumber} of ${question.totalQuestions}",
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
        )

        Spacer(Modifier.height(24.dp))

        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surfaceVariant
            )
        ) {
            Text(
                text = question.question,
                modifier = Modifier.padding(16.dp),
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.Medium
            )
        }

        Spacer(Modifier.height(24.dp))

        question.answers.forEach { answer ->
            OutlinedButton(
                onClick = { if (!isSubmitting) onAnswer(answer.id) },
                enabled = !isSubmitting,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 6.dp), // Increased vertical padding between buttons
                contentPadding = PaddingValues(16.dp) // Added internal padding to keep text away from rounded corners
            ) {
                Text(
                    text = answer.text,
                    textAlign = TextAlign.Start,
                    modifier = Modifier.fillMaxWidth(),
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
        
        Spacer(Modifier.height(32.dp))
    }
}

@Composable
private fun AnswerOverlay(
    result: AnswerResponse,
    onDismiss: () -> Unit
) {
    val bgColor = if (result.correct)
        MaterialTheme.colorScheme.primaryContainer
    else
        MaterialTheme.colorScheme.errorContainer

    val textColor = if (result.correct)
        MaterialTheme.colorScheme.onPrimaryContainer
    else
        MaterialTheme.colorScheme.onErrorContainer

    val scrollState = rememberScrollState()
    
    LaunchedEffect(result) {
        scrollState.scrollTo(0)
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = bgColor.copy(alpha = 0.98f)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(1f)) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(horizontal = 24.dp)
                        .verticalScroll(scrollState),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Top
                ) {
                    Spacer(Modifier.height(48.dp))
                    
                    Text(
                        text = if (result.correct) "Correct!" else "Incorrect",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = textColor
                    )

                    if (!result.correct) {
                        Spacer(Modifier.height(24.dp))
                        Text(
                            text = "The correct answer is:",
                            style = MaterialTheme.typography.labelLarge,
                            color = textColor.copy(alpha = 0.7f)
                        )
                        Text(
                            text = result.correctAnswer,
                            style = MaterialTheme.typography.bodyLarge,
                            fontWeight = FontWeight.SemiBold,
                            color = textColor,
                            textAlign = TextAlign.Center
                        )
                    }

                    result.explanation?.let { explanation ->
                        Spacer(Modifier.height(24.dp))
                        Text(
                            text = "Explanation:",
                            style = MaterialTheme.typography.labelLarge,
                            color = textColor.copy(alpha = 0.7f)
                        )
                        Text(
                            text = explanation,
                            style = MaterialTheme.typography.bodyMedium,
                            color = textColor,
                            textAlign = TextAlign.Center
                        )
                    }

                    Spacer(Modifier.height(24.dp))
                    Text(
                        text = "Score: ${result.score} / ${result.questionsAnswered}",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = textColor
                    )
                    
                    Spacer(Modifier.height(64.dp))
                }
            }

            Surface(
                modifier = Modifier.fillMaxWidth(),
                color = bgColor,
                tonalElevation = 8.dp,
                shadowElevation = 8.dp
            ) {
                Button(
                    onClick = onDismiss,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = textColor,
                        contentColor = bgColor
                    ),
                    modifier = Modifier
                        .padding(20.dp)
                        .fillMaxWidth()
                        .height(56.dp)
                ) {
                    Text(
                        text = if (result.isComplete) "View Results" else "Next Question",
                        style = MaterialTheme.typography.titleMedium
                    )
                }
            }
        }
    }
}
