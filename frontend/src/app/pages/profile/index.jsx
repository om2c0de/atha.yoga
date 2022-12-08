import React from 'react';
import { Navigate } from 'react-router-dom';

const ProfilePage = ({ auth: { user, tokens } }) => {
  if (!user) {
    return (
      <Navigate to="/login" />
    );
  }

  return (
    <div>
      <h2>Profile</h2>
      <p>
        <strong>Id: </strong>
        {user.id}
      </p>
      <p>
        <strong>Email: </strong>
        {user.email}
      </p>
      <p>
        <strong>Token: </strong>
        {tokens.access.substring(0, 20)}
      </p>
    </div>
  );
};

export default ProfilePage;
