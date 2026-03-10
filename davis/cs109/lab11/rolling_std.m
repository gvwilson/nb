%% Compose a function rolling_std which accepts as parameters an array
%  called `data` containing a row of time values and a row of measurements
%  and a window size `n`.
%
%  The function should return the resulting array of time points and
%  calculated rolling-window standard deviations.
%
function [ means ] = rolling_std( data, n )
    % test that the input is valid
    assert(n > 0,         'n should be positive.');
    assert(~mod(n,1),     'n should be an integer.');
    assert(~(mod(n,2)-1), 'n should be odd.');
    
    % YOU WRITE THIS CODE
    % It should be a straightforward modification of `rolling_mean`, using
    % the MATLAB standard deviation function.  To find this, use the `f_x`
    % button at the left of the prompt in the Command Window in MATLAB.
end