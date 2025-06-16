from math import pi
from pathlib import Path
from argparse import ArgumentParser
from msdsl import MixedSignalModel, VerilogGenerator, AnalogInput, AnalogOutput, AnalogSignal, Deriv

def main():
    print('Running model generator...')

    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', type=str, default='build')
    parser.add_argument('--dt', type=float, default=0.01e-6)  # 10 ps
    parser.add_argument('--adc_db', type=float, default=5.0)  # DC gain in dB
    parser.add_argument('--wp1_ghz', type=float, default=2.0) # pole 1 freq in GHz
    parser.add_argument('--wp2_ghz', type=float, default=8.0) # pole 2 freq in GHz
    args = parser.parse_args()

    # convert args
    adc = 10**(args.adc_db / 20)                  # linear gain from dB
    wp1 = 2 * pi * args.wp1_ghz * 1e9             # rad/s
    wp2 = 2 * pi * args.wp2_ghz * 1e9             # rad/s
    print(adc, wp1, wp2)

    # create the model
    model = MixedSignalModel('ctle', AnalogInput('v_in'), AnalogOutput('v_out'), dt=args.dt)
    model.add_analog_state('x', 100)    # output
    model.add_analog_state('dx', 100)   # derivative of output

    model.add_eqn_sys([
        # First pole dynamics
        Deriv(model.x) == -wp1 * model.x + model.v_in,
        
        # Second pole dynamics with zero effect
        Deriv(model.dx) == -wp2 * model.dx + wp2 * (model.x + adc * model.v_in),
        
        # Output equation
        model.v_out == model.dx
    ])

    # determine output filename
    filename = Path(args.output).resolve() / f'{model.module_name}.sv'
    print(f'Model will be written to: {filename}')

    # generate the model
    model.compile_to_file(VerilogGenerator(), filename)

if __name__ == '__main__':
    main()
