/* eslint-disable linebreak-style */
import React from 'react';
import {
  Typography, Box, Grid, Divider,
} from '@mui/material';
import DateRangeOutlinedIcon from '@mui/icons-material/DateRangeOutlined';
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined';

const ScheduleLessonCard = () => (
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
        fontSize: '18px', fontWeight: '500', p: '16px',
      }}
    >
      Мои занятия
    </Typography>
    <Box width="800px" m="16px" sx={{ border: '1px solid #E0E0E0', borderRadius: '8px' }}>
      <Grid container alignItems="center" justifyContent="center">
        <Grid item>
          <Typography sx={{ textAlign: 'center', p: '32px 16px 33px 20px', fontSize: '18px' }}>
            ВС
          </Typography>
        </Grid>
        <Divider orientation="vertical" variant="middle" sx={{ borderRight: '1px solid #0D6EFD' }} flexItem />
        <Grid item xs container>
          <Grid item xs container direction="column" sx={{ p: '16px' }}>
            <Grid item>
              <Typography sx={{ fontSize: '18px', mb: '8px' }}>
                Пранаяма
              </Typography>
            </Grid>
            <Grid item display="flex">
              <Typography color="text.secondary" mr="16px">
                <DateRangeOutlinedIcon fontSize="20" color="primary" sx={{ mr: '6px', verticalAlign: '-2px' }} />
                26.11
              </Typography>
              <Typography color="text.secondary">
                <AccessTimeOutlinedIcon fontSize="20" color="primary" sx={{ mr: '6px', verticalAlign: '-2px' }} />
                14:00 - 15:30
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  </Box>
);

export default ScheduleLessonCard;
