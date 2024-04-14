package routes

import (
	"net/http"
	"strconv"
	"web-server/entities"
	"web-server/usecases"

	"github.com/gin-gonic/gin"
)

func SetupRouter(userUC usecases.UserUseCase) *gin.Engine {

	router := gin.Default()

	//Get all users
	router.GET("/users", func(c *gin.Context) {
		users, err := userUC.GetAll()
		if err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "Failed to get Users"})
			return
		}

		c.IndentedJSON(http.StatusOK, users)
	})

	// Get Users by ID
	router.GET("/users/:id", func(c *gin.Context) {
		id, _ := strconv.Atoi(c.Param("id"))
		user, err := userUC.GetById(id)
		if err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "Failed to get user"})
			return
		}

		if user == nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "User not found"})
		}

		c.IndentedJSON(http.StatusOK, user)
	})

	router.POST("/users", func(c *gin.Context) {
		var user entities.User

		if err := c.ShouldBindJSON(&user); err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"error": "Invalid User Data"})
			return
		}

		if err := userUC.CreateNew(&user); err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "Failed to create user"})
			return
		}

		c.Status(http.StatusCreated)
	})

	router.DELETE("/user/:id", func(c *gin.Context) {
		id, _ := strconv.Atoi(c.Param("id"))
		if err := userUC.DeleteByID(id); err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete user"})
			return
		}

		c.Status(http.StatusOK)
	})

	return router
}
