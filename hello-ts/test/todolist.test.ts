describe('todo list', () => {
    test('just list of strings', () => {
        let stringArray: string[] = ['todo item'];

        stringArray.push('test');

        const result = stringArray[0]; // string
        expect(result).toEqual('todo item');
    })

    test('Item interface list', () => {
        interface todoItem {
            label: string;
            done: boolean;
        }

        let todoList: todoItem[] = [{label: 'test', done: true}];

        todoList.push({label: 'test2', done: true});
        let length = todoList.length;
        expect(length).toBe(2);
    })
})