define(['regs-data', 'samplejson'], function(RegsData, testjson) {
  describe("RegsData module", function() {
    RegsData.parse(testjson);

    it("should have a regStructure array", function() {
      expect(RegsData.regStructure).toBeTruthy();
    });

    it("should have a regStructure array with 10 values", function() {
      expect(RegsData.regStructure.length).toEqual( 10 );
    });

    it("should have content", function() {
      expect(RegsData.content).toBeTruthy(); 
    });

    it("should have content for 2345-9-a", function() {
      var content = "<p><dfn>placerat in egestas.</dfn> Sed erat enim, hendrerit mollis tempus et, consequat et ante. Donec imperdiet orci eget nisi lobortis molestie. Nullam pellentesque scelerisque hendrerit</p>";
      expect(RegsData.content['2345-9-a'].valueOf()).toEqual(content);
    });

    it("should get 2345-9", function() {
      expect(RegsData.get('2345-9')).toEqual("asdfksjflksjdf"); 
    });

    it("should get children", function() {
      var arr = ["2345-9-a-2", "2345-9-a-1"];

      expect(RegsData.getChildren('2345-9-a')).toEqual(arr);
    });

    it("should not get children", function() {
      expect(RegsData.getChildren('233')).toEqual([]);
    });

    it("should get parent", function() {
      expect(RegsData.getParent('2345-9-b')).toEqual("asdfksjflksjdf");
    });

    it("should differentiate between regStructure presence and being loaded", function() {
      expect(RegsData.has("2345-9-b-1")).toEqual(false);
    });

  });
});
