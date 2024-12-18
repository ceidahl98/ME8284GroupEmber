filename = 'N20-90RPM-1to298gr_1kHzTS.txt';
% filename = 'N20-90RPM-1to298gr_100HzTS.txt';
filename = 'putty222259.log';
filename = 'putty101204.log';
filename = 'putty105948.log';


filename = 'putty111751.log';
% filename = 'putty131718.log';
% filename = 'putty215027.log';
% filename = 'putty222149.log';

%D = load(filename);
DD = importdata(filename); % more robust that load
DD.textdata
D = DD.data;





GR = 298;  % Gear Ratio between servo pulley and load

t = D(:,1)  / 1000; % convert to [s]
u = D(:,2);
enc = D(:,3);
pos = D(:,4);
% vel = D(:,5);
% acc = D(:,6);
tt = D(:,end);

figure(10); clf
plot(t, u, 'DisplayName','command u [deg]'); hold on;
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
plot(t, pos, '.','DisplayName','position [deg]'); hold on;
xlabel('time [s]'); legend(); 
title(filename)

figure(11);
clf
vel = [0 ; diff(pos)]./diff([0 ; t]);
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
yyaxis left;
plot(t, vel, 'DisplayName','vel [deg/s]'); hold on;
yyaxis right;
plot(t, u, 'DisplayName','command [pwm]');
xlabel('time [ms]'); legend(); 
title(filename)

figure(12);
clf
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
plot(pos, vel , '.'); hold on;
xlabel('pos [deg]'); ylabel('vel [deg/s]');legend(); 
title(filename)


figure(13);
clf
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
plot(u, vel ,'.'); hold on;
xlabel('u [pwm]'); ylabel('vel [deg/s]');legend(); 
title(filename)

figure(14);
clf
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
% scatter3(pos, u, vel, '.' ); hold on;
scatter3(mod(pos,360), u, vel, '.' ); hold on;
zlim([0 10])
xlabel('pos [deg]');ylabel('u [pwm]'); zlabel('vel [deg/s]');legend(); 
title(filename)



% Plot along wave period only
figure(33);
clf
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
yyaxis left;
plot(tt, vel, '.', 'DisplayName','vel [deg/s]'); hold on;
ylabel('vel [deg/s]');
yyaxis right;
plot(tt, u,'.',  'DisplayName','command [pwm]', 'markersize', 2);
xlabel('time [s]'); legend(); 
ylabel('u [PWM]');
title('Step Response Sweep'); grid on

% try plotting just steady states.  
figure (34);clf
ii = find ( (tt > 980) & (tt <1000));
plot( u(ii), vel(ii), '.' );
xlabel('u [PWM]'); ylabel( 'vel [deg/s] ')
title('Steady State Behavior'); grid on

%% Plot Jitter

figure(22);clf
subplot(2,1,1);
hist(diff(t(1:end)), 25);
xlabel('Sample Period [ms]')
subplot(2,1,2);
plot( diff(t(1:end/1))); xlabel('time[ms]'); ylabel('deltaT')

%% Extract Settling time and rise time
TT = max(tt); % period of square
TT0 = floor(TT/2);
N = length(find(t<TT/1000)); % length of each period in samples

C = 1-exp(-1);  % 63.2% for time constant
TimeConstants = [];

for i =1:length(t) / N ;% for each period T
    j = [1 : N] + N*(i-1);  
    j = j( find( u(j) > 0 , 1 ) : end);
    tRange = t(j); velRange = vel(j);  uRange = u(j);
    %uRange(1:10)';
    Vel63 = C*max( velRange ); 
    i63 = find( velRange >= Vel63, 1); % first time Vel exceeds 63%   
    tc = tRange(i63) - tRange(1);
    figure;(44); clf;
    plot(tRange, velRange, '-'); hold on
    plot(tRange(i63), velRange(i63), 'r.', 'markersize', 20); % Time constant
    hold on; plot(tRange(i63), uRange(i63), 'g.', 'markerSize', 20 );
    legend('response', 'time constant', 'pwm command')
    axis tight    
    
    TimeConstants = [TimeConstants; tc uRange(i63) velRange(i63) i63];
end
TimeConstants
figure(54);clf
plot(TimeConstants(:, 2), TimeConstants(:,1),  '.'); hold on
xlabel('u [PWM]'); ylabel( 'Time Constant (63.2%) [s] ' )
title('Time Constants Depends on Amplitude'); grid on
%% Now try a chirp
return
fn ='TowerProMG996r_chirp.txt'
fn ='Sevro SAVOX 1285tg digital _chirp.txt'
D = load(fn );

t = D(:,1)  / 1000; % convert to [s]
u = D(:,2);
enc = D(:,3);
pos = D(:,4);
vel = D(:,5);
acc = D(:,6);

figure(21); clf
plot(t, u/GR, 'DisplayName','command u [deg]'); hold on;
% plot(t, enc, 'DisplayName','encoder pos [ticks]'); hold on;
plot(t, pos, 'DisplayName','position [deg]'); hold on;
xlabel('time [s]'); legend(); 
title (fn)

