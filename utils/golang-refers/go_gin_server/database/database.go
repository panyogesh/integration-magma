package database

import (
	"web-server/entities"
)

type UserDB interface {
	GetAll() ([]*entities.User, error)
	GetById(id int) (*entities.User, error)
	CreateNew(user *entities.User) error
	DeleteByID(id int) error
}
