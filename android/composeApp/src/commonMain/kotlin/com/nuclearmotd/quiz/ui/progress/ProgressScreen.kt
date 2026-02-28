package com.nuclearmotd.quiz.ui.progress

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ProgressResponse
import com.nuclearmotd.quiz.data.api.CategoryProgress
import kotlin.math.roundToInt

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProgressScreen(
    onBack: () -> Unit,
    vm: ProgressViewModel = viewModel()
) {
    val progressState by vm.progressState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My Progress") },
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
                .padding(innerPadding),
            contentAlignment = Alignment.Center
        ) {
            when (val state = progressState) {
                is UiState.Loading -> CircularProgressIndicator()
                is UiState.Error -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(state.message, color = MaterialTheme.colorScheme.error)
                        Spacer(Modifier.height(8.dp))
                        Button(onClick = { vm.loadProgress() }) { Text("Retry") }
                    }
                }
                is UiState.Success -> ProgressContent(progress = state.data)
            }
        }
    }
}

@Composable
private fun ProgressContent(progress: ProgressResponse) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Overall Accuracy",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Text(
                        text = "${progress.overall.accuracy.roundToInt()}%",
                        style = MaterialTheme.typography.headlineLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Text(
                        text = "${progress.overall.totalCorrect} / ${progress.overall.totalAnswered} correct answers",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.7f)
                    )
                }
            }
        }

        item {
            Spacer(Modifier.height(8.dp))
            Text(
                text = "Performance by Category",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
        }

        items(progress.byCategory) { category ->
            CategoryProgressCard(category = category)
        }
    }
}

@Composable
private fun CategoryProgressCard(category: CategoryProgress) {
    val accuracy = category.accuracy.roundToInt()
    
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = category.categoryName,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.weight(1f)
                )
                Text(
                    text = "$accuracy%",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = when {
                        accuracy >= 80 -> MaterialTheme.colorScheme.primary
                        accuracy >= 50 -> MaterialTheme.colorScheme.secondary
                        else -> MaterialTheme.colorScheme.error
                    }
                )
            }
            
            Spacer(Modifier.height(8.dp))
            
            LinearProgressIndicator(
                progress = { category.accuracy.toFloat() / 100f },
                modifier = Modifier.fillMaxWidth(),
                color = when {
                    accuracy >= 80 -> MaterialTheme.colorScheme.primary
                    accuracy >= 50 -> MaterialTheme.colorScheme.secondary
                    else -> MaterialTheme.colorScheme.error
                }
            )
            
            Spacer(Modifier.height(4.dp))
            
            Text(
                text = "${category.totalCorrect} correct of ${category.totalAnswered} answered",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
            )
        }
    }
}
