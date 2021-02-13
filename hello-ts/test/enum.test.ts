describe('basic types', () => {
    test('Enum number', () => {
        enum Color {
            Red,
            Green,
            Blue
        };

        let c: Color = Color.Green;
        expect(c).toBe(1);
    })

    test('Enum name', () => {
        enum Color {
            Red=1,
            Green,
            Blue
        }
        let colorName: string = Color[2];
        expect(colorName).toBe('Green');
    })
    test('Enum counter', () => {
        enum Color {
            red,
            green,
            blue
        }

        const colorList: Color[] = [
            Color.red, Color.green,
            Color.red, Color.green, Color.red
        ];
        
        function keysOfEnum(enumObj: object): string[] {
            return Object.keys(enumObj)
                .filter(key=>isNaN(parseInt(key)));
        }
            
        function count<T>(list: T[] , expected: T): number {
            return list.filter(v=>v==expected).length
        };

        type EnumCounter = { [key: string]: number};

        function enumCounter<T>(
            enumObj: object, enumList: T[]
        ): EnumCounter {
            const initial: EnumCounter = {};
            return keysOfEnum(enumObj).reduce((result, color)=>({
                ...result,
                [color]: count(enumList, enumObj[color])
            }), initial);
        }
        
        const colorsCount = enumCounter(Color, colorList);
        console.log(colorsCount);
        expect(colorsCount.red).toBe(3);
        expect(colorsCount.green).toBe(2);
        expect(colorsCount.blue).toBe(0);
    })
})

