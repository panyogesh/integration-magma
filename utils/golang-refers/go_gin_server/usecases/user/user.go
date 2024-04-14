package usecases

import (
	"web-server/database"
	"web-server/entities"
)

type UserUseCase struct {
	DB database.UserDB
}

func NewUserUseCase(userRepo database.UserDB) *UserUseCase {
	return &UserUseCase{
		DB: userRepo,
	}
}

func (uc *UserUseCase) GetAll() ([]*entities.User, error) {
	return uc.DB.GetAll()
}

func (uc *UserUseCase) GetById(id int) (*entities.User, error) {
	return uc.DB.GetById(id)
}

func (uc *UserUseCase) CreateNew(user *entities.User) error {
	return uc.DB.CreateNew(user)
}

func (uc *UserUseCase) DeleteByID(id int) error {
	return uc.DB.DeleteByID(id)
}
