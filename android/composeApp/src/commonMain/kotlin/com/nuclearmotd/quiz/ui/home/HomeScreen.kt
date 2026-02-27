package com.nuclearmotd.quiz.ui.home

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.Category

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onQuizStart: (String) -> Unit,
    onProgressClick: () -> Unit,
    onAccountClick: () -> Unit,
    onLogout: () -> Unit,
    vm: HomeViewModel = viewModel()
) {
    val categoriesState by vm.categories.collectAsState()
    val startQuizState by vm.startQuizState.collectAsState()

    LaunchedEffect(startQuizState) {
        if (startQuizState is UiState.Success) {
            val quizId = (startQuizState as UiState.Success<String>).data
            onQuizStart(quizId)
            vm.resetStartState()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Nuclear Quiz") },
                actions = {
                    IconButton(onClick = onProgressClick) {
                        Icon(Icons.Default.Refresh, contentDescription = "Progress")
                    }
                    IconButton(onClick = onAccountClick) {
                        Icon(Icons.Default.AccountCircle, contentDescription = "Account")
                    }
                    IconButton(onClick = {
                        vm.logout()
                        onLogout()
                    }) {
                        Icon(Icons.Default.ExitToApp, contentDescription = "Logout")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            Text(
                text = "Welcome back, ${vm.username}!",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )

            Spacer(Modifier.height(16.dp))

            OutlinedButton(
                onClick = { vm.startQuiz(null) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Start Random Quiz (10 questions)")
            }

            Spacer(Modifier.height(16.dp))

            Text(
                text = "Or pick a category:",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
            )

            Spacer(Modifier.height(8.dp))

            when (val state = categoriesState) {
                is UiState.Loading -> {
                    Box(Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                is UiState.Error -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = state.message,
                            color = MaterialTheme.colorScheme.error,
                            textAlign = TextAlign.Center
                        )
                        Spacer(Modifier.height(8.dp))
                        Button(onClick = { vm.loadCategories() }) { Text("Retry") }
                    }
                }
                is UiState.Success -> {
                    LazyVerticalGrid(
                        columns = GridCells.Fixed(2),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        items(state.data) { category ->
                            CategoryCard(
                                category = category,
                                onClick = { vm.startQuiz(category.id) }
                            )
                        }
                    }
                }
            }

            if (startQuizState is UiState.Loading) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }
            if (startQuizState is UiState.Error) {
                Text(
                    text = (startQuizState as UiState.Error).message,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}

@Composable
private fun CategoryCard(category: Category, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = category.name,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = "${category.questionCount} questions",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.7f)
            )
        }
    }
}
