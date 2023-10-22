import "jasmine";
import { makeRoutes } from '../src/routes';

const { Views } = makeRoutes("");

describe("Views route", () => {
    it("should be immutable", () => {
        const original = Views.Wishlist.to_string();
        Views.Wishlist.append(2);
        expect(Views.Wishlist.to_string()).toEqual(original);
    });
});
