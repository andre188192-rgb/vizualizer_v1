import re


class GCodeParser:
    def __init__(self):
        self.position = {'X': 0, 'Y': 0, 'Z': 0}
        self.units = 'mm'
        self.mode = 'absolute'

    def parse_gcode(self, gcode):
        lines = gcode.split('\n')
        commands = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            # Удаляем комментарии
            if ';' in line:
                line = line.split(';')[0].strip()

            match = re.match(r'([GM]\d+)(.*)', line)
            if match:
                cmd, args = match.groups()
                params = {}
                for arg in re.findall(r'([A-Z])([-\d.]+)', args):
                    key, val = arg
                    params[key] = float(val)
                commands.append({'command': cmd, 'params': params})
        return commands

    def parse_to_json(self, gcode_text):
        """Parse G-code text into a JSON-ready structure for the Godot client."""
        commands = []
        current_position = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        units = 'mm'
        mode = 'absolute'
        bounds_min = [0.0, 0.0, 0.0]
        bounds_max = [0.0, 0.0, 0.0]

        def to_mm(value):
            if units == 'inch':
                return value * 25.4
            return value

        lines = gcode_text.split('\n')
        for index, raw_line in enumerate(lines, start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith(';'):
                continue
            if ';' in stripped:
                stripped = stripped.split(';')[0].strip()
            match = re.match(r'([GM]\d+)(.*)', stripped)
            if not match:
                continue
            cmd, args = match.groups()
            params = {}
            for arg in re.findall(r'([A-Z])([-\d.]+)', args):
                key, val = arg
                params[key] = float(val)

            cmd_upper = cmd.upper()
            cmd_type = 'other'
            if cmd_upper == 'G0':
                cmd_type = 'rapid'
            elif cmd_upper == 'G1':
                cmd_type = 'linear'
            elif cmd_upper == 'G2':
                cmd_type = 'arc_cw'
            elif cmd_upper == 'G3':
                cmd_type = 'arc_ccw'
            elif cmd_upper == 'M3':
                cmd_type = 'tool_on'
            elif cmd_upper == 'M5':
                cmd_type = 'tool_off'

            if cmd_upper == 'G20':
                units = 'inch'
            elif cmd_upper == 'G21':
                units = 'mm'
            elif cmd_upper == 'G90':
                mode = 'absolute'
            elif cmd_upper == 'G91':
                mode = 'relative'

            target = current_position.copy()
            if cmd_type in {'rapid', 'linear', 'arc_cw', 'arc_ccw'}:
                for axis in ('X', 'Y', 'Z'):
                    if axis in params:
                        value = to_mm(params[axis])
                        if mode == 'absolute':
                            target[axis] = value
                        else:
                            target[axis] = current_position[axis] + value

                current_position = target

            end_point = {
                'x': current_position['X'],
                'y': current_position['Y'],
                'z': current_position['Z'],
            }

            bounds_min[0] = min(bounds_min[0], end_point['x'])
            bounds_min[1] = min(bounds_min[1], end_point['y'])
            bounds_min[2] = min(bounds_min[2], end_point['z'])
            bounds_max[0] = max(bounds_max[0], end_point['x'])
            bounds_max[1] = max(bounds_max[1], end_point['y'])
            bounds_max[2] = max(bounds_max[2], end_point['z'])

            feedrate = None
            if 'F' in params:
                feedrate = to_mm(params['F'])

            command_entry = {
                'line': index,
                'type': cmd_type,
                'end': end_point,
                'feedrate': feedrate,
                'raw': stripped,
            }
            if cmd_type in {'arc_cw', 'arc_ccw'}:
                arc_params = {
                    'i': to_mm(params.get('I', 0.0)),
                    'j': to_mm(params.get('J', 0.0)),
                }
                if 'K' in params:
                    arc_params['k'] = to_mm(params['K'])
                command_entry['arc_params'] = arc_params
            commands.append(command_entry)

        workflow = ['G90' if mode == 'absolute' else 'G91', 'G21' if units == 'mm' else 'G20']

        return {
            'metadata': {
                'total_commands': len(commands),
                'bounds': {
                    'min': bounds_min,
                    'max': bounds_max,
                },
                'units': units,
                'workflow': workflow,
            },
            'commands': commands,
        }


if __name__ == "__main__":
    parser = GCodeParser()
    with open("test.gcode", "r") as f:
        result = parser.parse_to_json(f.read())
    import json

    print(json.dumps(result, indent=2))
