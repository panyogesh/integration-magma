package database

import "web-server/entities"

type UserDB struct {
	users []*entities.User
}

func NewUserDB() *UserDB {
	return &UserDB{
		users: []*entities.User{
			{
				ID:   1,
				Name: "ABC",
			},
			{
				ID:   2,
				Name: "DEF",
			},
			{
				ID:   3,
				Name: "GHI",
			},
			{
				ID:   4,
				Name: "JKL",
			},
		},
	}
}

func (repo *UserDB) GetAll() ([]*entities.User, error) {
	return repo.users, nil
}

func (repo *UserDB) GetById(ID int) (*entities.User, error) {
	for _, user := range repo.users {
		if user.ID == ID {
			return user, nil
		}
	}

	return nil, nil
}

func (repo *UserDB) CreateNew(user *entities.User) error {
	repo.users = append(repo.users, user)
	return nil
}

func (repo *UserDB) DeleteByID(ID int) error {
	for i, user := range repo.users {
		if user.ID == ID {
			repo.users = append(repo.users[:i], repo.users[i+1:]...)
			return nil
		}
	}

	return nil
}
