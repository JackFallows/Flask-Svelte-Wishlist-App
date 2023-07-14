import "jasmine";
import { Route, Views, Api } from '../src/routes';

describe("Views route", () => {
    it("should be immutable", () => {
        const original = Views.Edit.to_string();
        Views.Edit.append(2);
        expect(Views.Edit.to_string()).toEqual(original);
    });
});
