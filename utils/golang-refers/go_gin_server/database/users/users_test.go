package database_test

import (
	"testing"
	database "web-server/database/users"
	"web-server/entities"
)

func TestUserDB(t *testing.T) {
	// Create a new instance of UserDB
	userDB := database.NewUserDB()

	// Test GetAll method
	t.Run("GetAll", func(t *testing.T) {
		users, err := userDB.GetAll()

		if err != nil {
			t.Errorf("GetAll returned an unexpected error: %v", err)
		}

		if len(users) != 4 {
			t.Errorf("GetAll returned wrong number of users: got %d, want %d", len(users), 4)
		}
	})

	// Test GetById method
	t.Run("GetById", func(t *testing.T) {
		expectedUser := &entities.User{ID: 2, Name: "DEF"}
		user, err := userDB.GetById(2)

		if err != nil {
			t.Errorf("GetById returned an unexpected error: %v", err)
		}

		if user == nil || user.ID != expectedUser.ID || user.Name != expectedUser.Name {
			t.Errorf("GetById returned wrong user: got %v, want %v", user, expectedUser)
		}
	})

	// Test CreateNew method
	t.Run("CreateNew", func(t *testing.T) {
		newUser := &entities.User{ID: 5, Name: "MNO"}
		err := userDB.CreateNew(newUser)

		if err != nil {
			t.Errorf("CreateNew returned an unexpected error: %v", err)
		}

		// Check if the user was actually added
		users, _ := userDB.GetAll()
		found := false
		for _, user := range users {
			if user.ID == newUser.ID && user.Name == newUser.Name {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("CreateNew did not add the user: %v", newUser)
		}
	})

	// Test DeleteByID method
	t.Run("DeleteByID", func(t *testing.T) {
		err := userDB.DeleteByID(3)

		if err != nil {
			t.Errorf("DeleteByID returned an unexpected error: %v", err)
		}

		// Check if the user was actually deleted
		users, _ := userDB.GetAll()
		found := false
		for _, user := range users {
			if user.ID == 3 {
				found = true
				break
			}
		}
		if found {
			t.Errorf("DeleteByID did not delete the user with ID 3")
		}
	})
}
