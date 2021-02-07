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
    test('Enum count', () => {
        enum Color {
            red,
            green,
            blue
        }

        const colorList: Color[] = [
            Color.red, Color.green, Color.blue,
            Color.red, Color.blue, Color.red
        ];

        
        const colorKeys: string[] = Object.keys(Color)
            .filter(key=>isNaN(parseInt(key)));
            
        function count<T>(list: T[] , expected: T): number {
            return list.filter(v=>v==expected).length
        };
        
        const initial: { [key: string]: number} = {};

        const colorsCount = colorKeys.reduce((result, color)=>({
            ...result,
            [color]: count(colorList, Color[color])
        }), initial);

        console.log(Color);
        console.log(colorsCount);
        expect(colorsCount.red).toBe(3);
        expect(colorsCount.green).toBe(1);
        expect(colorsCount.blue).toBe(2);
    })
})

