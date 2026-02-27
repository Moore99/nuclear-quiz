package com.nuclearmotd.quiz.nav

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.toRoute
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.ui.auth.AccountManagementScreen
import com.nuclearmotd.quiz.ui.auth.AuthScreen
import com.nuclearmotd.quiz.ui.auth.ResetPasswordScreen
import com.nuclearmotd.quiz.ui.home.HomeScreen
import com.nuclearmotd.quiz.ui.progress.ProgressScreen
import com.nuclearmotd.quiz.ui.quiz.QuizScreen
import com.nuclearmotd.quiz.ui.quiz.ResultsScreen
import com.nuclearmotd.quiz.ui.quiz.ReviewScreen
import kotlinx.serialization.Serializable

@Serializable object AuthRoute
@Serializable object HomeRoute
@Serializable data class QuizRoute(val quizId: String)
@Serializable data class ResultsRoute(val quizId: String)
@Serializable object ProgressRoute
@Serializable object ResetPasswordRoute
@Serializable object AccountManagementRoute
@Serializable data class ReviewRoute(val quizId: String)

@Composable
fun NavGraph(navController: NavHostController) {
    val startDestination: Any =
        if (AppDependencies.tokenStore.isLoggedIn()) HomeRoute else AuthRoute

    NavHost(navController = navController, startDestination = startDestination) {

        composable<AuthRoute> {
            AuthScreen(
                onAuthSuccess = {
                    navController.navigate(HomeRoute) {
                        popUpTo<AuthRoute> { inclusive = true }
                    }
                },
                onForgotPassword = {
                    navController.navigate(ResetPasswordRoute)
                }
            )
        }

        composable<ResetPasswordRoute> {
            ResetPasswordScreen(
                onBack = { navController.popBackStack() },
                onSuccess = {
                    navController.popBackStack()
                }
            )
        }

        composable<HomeRoute> {
            HomeScreen(
                onQuizStart = { quizId ->
                    navController.navigate(QuizRoute(quizId))
                },
                onProgressClick = {
                    navController.navigate(ProgressRoute)
                },
                onAccountClick = {
                    navController.navigate(AccountManagementRoute)
                },
                onLogout = {
                    navController.navigate(AuthRoute) {
                        popUpTo<HomeRoute> { inclusive = true }
                    }
                }
            )
        }

        composable<AccountManagementRoute> {
            AccountManagementScreen(
                onBack = { navController.popBackStack() },
                onAccountDeleted = {
                    navController.navigate(AuthRoute) {
                        popUpTo(0) { inclusive = true }
                    }
                }
            )
        }

        composable<QuizRoute> { backStackEntry ->
            val route = backStackEntry.toRoute<QuizRoute>()
            QuizScreen(
                quizId = route.quizId,
                onComplete = { id ->
                    navController.navigate(ResultsRoute(id)) {
                        popUpTo<QuizRoute> { inclusive = true }
                    }
                },
                onBack = { navController.popBackStack() }
            )
        }

        composable<ResultsRoute> { backStackEntry ->
            val route = backStackEntry.toRoute<ResultsRoute>()
            ResultsScreen(
                quizId = route.quizId,
                onHome = {
                    navController.navigate(HomeRoute) {
                        popUpTo<HomeRoute> { inclusive = true }
                    }
                },
                onReview = {
                    navController.navigate(ReviewRoute(route.quizId))
                }
            )
        }

        composable<ReviewRoute> { backStackEntry ->
            val route = backStackEntry.toRoute<ReviewRoute>()
            ReviewScreen(
                quizId = route.quizId,
                onBack = { navController.popBackStack() }
            )
        }

        composable<ProgressRoute> {
            ProgressScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}
