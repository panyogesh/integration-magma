package routes

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"web-server/entities"
	routes "web-server/routes/users"
)

// MockUserUseCase is a mock implementation of the UserUseCase interface
type MockUserUseCase struct{}

func (m *MockUserUseCase) GetAll() ([]*entities.User, error) {
	// Return a sample list of users
	return []*entities.User{{ID: 1, Name: "John"}, {ID: 2, Name: "Jane"}}, nil
}

func (m *MockUserUseCase) GetById(id int) (*entities.User, error) {
	// Return a sample user by ID
	if id == 1 {
		return &entities.User{ID: 1, Name: "John"}, nil
	}
	return nil, nil
}

func (m *MockUserUseCase) CreateNew(user *entities.User) error {
	// Mock implementation for creating a new user
	return nil
}

func (m *MockUserUseCase) DeleteByID(id int) error {
	// Mock implementation for deleting a user by ID
	return nil
}

func TestSetupRouter(t *testing.T) {
	// Create a new instance of the mock user use case
	mockUserUC := &MockUserUseCase{}

	// Setup the router with the mock user use case
	router := routes.SetupRouter(mockUserUC)

	// Create a new HTTP request to test the /users endpoint
	req, err := http.NewRequest("GET", "/users", nil)
	if err != nil {
		t.Fatal(err)
	}

	// Create a response recorder to record the response
	rec := httptest.NewRecorder()

	// Serve the HTTP request to the router
	router.ServeHTTP(rec, req)

	// Check the status code of the response
	if status := rec.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Check the response body
	expected := `[{"ID":1,"Name":"John"},{"ID":2,"Name":"Jane"}]`
	if rec.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v",
			rec.Body.String(), expected)
	}
}
