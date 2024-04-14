package main

import (
	userDatabase "web-server/database/users"
	userRouter "web-server/routes/users"
	userUseCase "web-server/usecases/user"
)

func main() {
	// Initialize reposistory
	userDB := userDatabase.NewUserDB()

	// Initialize new Usecases
	userUC := userUseCase.NewUserUseCase(userDB)

	// Setup router
	router := userRouter.SetupRouter(userUC)

	// Run the router
	router.Run(":8080")
}
