alter table auth_user
add column has_to_change_password boolean NOT NULL,
add column last_password_change timestamp NOT NULL,
add column password_expires timestamp NOT NULL