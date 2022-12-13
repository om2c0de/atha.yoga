/* eslint-disable linebreak-style */
import React from 'react';
import {
  Typography, Box, Grid, Divider,
} from '@mui/material';
import DateRangeOutlinedIcon from '@mui/icons-material/DateRangeOutlined';
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined';

const Calendar = () => (
  <Box
    sx={{
      marginTop: 6,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}
  >
    <Typography
      color="primary"
      sx={{
        fontSize: '16px', fontWeight: '600', p: '16px',
      }}
    >
      Мои занятия
    </Typography>
    <Box width="80%" m="16px" sx={{ border: '1px solid #E0E0E0', borderRadius: '8px' }}>
      <Grid container alignItems="center" justifyContent="center">
        <Grid item>
          <Typography sx={{ textAlign: 'center', p: '32px 16px 33px 20px', fontSize: '18px' }}>
            ВС
          </Typography>
        </Grid>
        <Divider orientation="vertical" variant="middle" flexItem />
        <Grid item xs container>
          <Grid item xs container direction="column" sx={{ p: '16px' }}>
            <Grid item>
              <Typography sx={{ fontSize: '18px' }}>
                Пранаяма
              </Typography>
            </Grid>
            <Grid item display="flex">
              <Typography color="text.secondary" mr="16px">
                <DateRangeOutlinedIcon fontSize="20" color="primary" />
                26.11
              </Typography>
              <Typography color="text.secondary">
                <AccessTimeOutlinedIcon fontSize="20" color="primary" />
                14:00 - 15:30
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  </Box>
);

export default Calendar;
