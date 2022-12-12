import React from 'react';
import { Navigate } from 'react-router-dom';
import Profile from '../../components/profile';

const ProfilePage = ({ auth: { user } }) => {
/*
  if (!user) {
    return (
      <Navigate to="/login" />
    );
  }
*/

  return (
    <Profile user={user} />
  );
};

export default ProfilePage;
