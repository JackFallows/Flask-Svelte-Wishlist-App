import "jasmine";
import { makeRoutes } from '../src/routes';

const { Views } = makeRoutes("");

describe("Views route", () => {
    it("should be immutable", () => {
        const original = Views.Wishlist.Edit.to_string();
        Views.Wishlist.Edit.append(2);
        expect(Views.Wishlist.Edit.to_string()).toEqual(original);
    });
});
