import React from 'react';
import { Outlet } from 'react-router-dom';
import { Grid } from '@mui/material';
import Menu from '../../components/menu';

const ProfileLayout = ({ auth }) => (
  <Grid
    container
    justifyContent="flex-start"
    alignItems="flex-start"
    spacing={2}
    sx={{ paddingTop: '20px' }}
  >
    <Grid
      item
      md={2.5}
      sm={1}
      sx={{
        justifyContent: 'center', display: 'flex', borderRight: '1px solid #DCDCDC',
      }}
    >
      <Menu auth={auth} />
    </Grid>

    <Grid item md={6} sm={1} container>
      <Outlet />
    </Grid>
  </Grid>
);

export default ProfileLayout;
